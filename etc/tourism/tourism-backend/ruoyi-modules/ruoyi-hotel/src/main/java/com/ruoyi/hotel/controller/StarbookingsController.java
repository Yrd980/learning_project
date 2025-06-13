package com.ruoyi.hotel.controller;

import java.util.ArrayList;
import java.util.List;
import javax.servlet.http.HttpServletResponse;

import com.ruoyi.hotel.domain.Nonstarbookings;
import com.ruoyi.hotel.domain.VO.bookingVO;
import com.ruoyi.hotel.service.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.log.annotation.Log;
import com.ruoyi.common.log.enums.BusinessType;
import com.ruoyi.common.security.annotation.RequiresPermissions;
import com.ruoyi.hotel.domain.Starbookings;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 星级酒店预定信息Controller
 * 
 * @author ningf
 * @date 2024-07-11
 */
@RestController
@RequestMapping("/starbookings")
public class StarbookingsController extends BaseController
{
    @Autowired
    private IStarbookingsService starbookingsService;

    @Autowired
    private INonstarbookingsService nonstarbookingsService;

    @Autowired
    private IStarhotelsService starhotelsService;

    @Autowired
    private INonstarhotelsService nonstarhotelsService;

    @Autowired
    private IStarroomtypesService starroomtypesService;

    @Autowired
    private INonstarroomtypesService nonstarroomtypesService;

    @GetMapping("/listall")
    public TableDataInfo listall(Starbookings starbookings)
    {
        Nonstarbookings nonstarbookings =new Nonstarbookings();
        startPage();
        List<bookingVO> result = new ArrayList<>();
        List<Starbookings> list = starbookingsService.selectStarbookingsList(starbookings);
        List<Nonstarbookings> nlist = nonstarbookingsService.selectNonstarbookingsList(nonstarbookings);
        list.forEach(item ->{
            bookingVO bookingvo = new bookingVO();
            bookingvo.setHotelName(starhotelsService.selectStarhotelsById(item.getHotelId()).getName());
            bookingvo.setRoomTypeName(starroomtypesService.selectStarroomtypesById(item.getRoomTypeId()).getName());
            bookingvo.setGuestId(item.getGuestId());
            bookingvo.setContactNumber(item.getContactNumber());
            bookingvo.setRecorded(item.getRecorded());
            bookingvo.setCheckInTime(item.getCheckInTime());
            bookingvo.setCheckOutTime(item.getCheckOutTime());
            bookingvo.setGuestName(item.getGuestName());
            result.add(bookingvo);
        });
        nlist.forEach(item ->{
            bookingVO bookingvo = new bookingVO();
            bookingvo.setHotelName(nonstarhotelsService.selectNonstarhotelsById(item.getHotelId()).getName());
            bookingvo.setRoomTypeName(nonstarroomtypesService.selectNonstarroomtypesById(item.getRoomTypeId()).getName());
            bookingvo.setGuestId(item.getGuestId());
            bookingvo.setContactNumber(item.getContactNumber());
            bookingvo.setRecorded(item.getRecorded());
            bookingvo.setCheckInTime(item.getCheckInTime());
            bookingvo.setCheckOutTime(item.getCheckOutTime());
            bookingvo.setGuestName(item.getGuestName());
            result.add(bookingvo);
        });
        return getDataTable(result);
    }

    /**
     * 查询星级酒店预定信息列表
     */
    @RequiresPermissions("hotel:starbookings:list")
    @GetMapping("/list")
    public TableDataInfo list(Starbookings starbookings)
    {
        startPage();
        List<Starbookings> list = starbookingsService.selectStarbookingsList(starbookings);
        return getDataTable(list);
    }

    /**
     * 导出星级酒店预定信息列表
     */
    @RequiresPermissions("hotel:starbookings:export")
    @Log(title = "星级酒店预定信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Starbookings starbookings)
    {
        List<Starbookings> list = starbookingsService.selectStarbookingsList(starbookings);
        ExcelUtil<Starbookings> util = new ExcelUtil<Starbookings>(Starbookings.class);
        util.exportExcel(response, list, "星级酒店预定信息数据");
    }

    /**
     * 获取星级酒店预定信息详细信息
     */
    @RequiresPermissions("hotel:starbookings:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(starbookingsService.selectStarbookingsById(id));
    }

    /**
     * 新增星级酒店预定信息
     */
    @RequiresPermissions("hotel:starbookings:add")
    @Log(title = "星级酒店预定信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Starbookings starbookings)
    {
        return toAjax(starbookingsService.insertStarbookings(starbookings));
    }

    /**
     * 修改星级酒店预定信息
     */
    @RequiresPermissions("hotel:starbookings:edit")
    @Log(title = "星级酒店预定信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Starbookings starbookings)
    {
        return toAjax(starbookingsService.updateStarbookings(starbookings));
    }

    /**
     * 删除星级酒店预定信息
     */
    @RequiresPermissions("hotel:starbookings:remove")
    @DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(starbookingsService.deleteStarbookingsByIds(ids));
    }

    /**
     * 删除星级酒店预定信息
     */
    @RequiresPermissions("hotel:starbookings:remove")
    @DeleteMapping("/confirm/{ids}")
    public AjaxResult Confirm(@PathVariable Long[] ids)
    {
        return toAjax(starbookingsService.confirmStarbookingsByIds(ids));
    }
}

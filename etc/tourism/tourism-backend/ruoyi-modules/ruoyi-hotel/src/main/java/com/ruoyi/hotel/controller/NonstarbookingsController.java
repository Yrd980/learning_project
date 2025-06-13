package com.ruoyi.hotel.controller;

import java.util.List;
import java.io.IOException;
import javax.servlet.http.HttpServletResponse;
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
import com.ruoyi.hotel.domain.Nonstarbookings;
import com.ruoyi.hotel.service.INonstarbookingsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 非星级酒店预定信息Controller
 * 
 * @author ningf
 * @date 2024-07-14
 */
@RestController
@RequestMapping("/nonstarbookings")
public class NonstarbookingsController extends BaseController
{
    @Autowired
    private INonstarbookingsService nonstarbookingsService;

    /**
     * 查询非星级酒店预定信息列表
     */
    @RequiresPermissions("hotel:nonstarbookings:list")
    @GetMapping("/list")
    public TableDataInfo list(Nonstarbookings nonstarbookings)
    {
        startPage();
        List<Nonstarbookings> list = nonstarbookingsService.selectNonstarbookingsList(nonstarbookings);
        return getDataTable(list);
    }

    /**
     * 导出非星级酒店预定信息列表
     */
    @RequiresPermissions("hotel:nonstarbookings:export")
    @Log(title = "非星级酒店预定信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Nonstarbookings nonstarbookings)
    {
        List<Nonstarbookings> list = nonstarbookingsService.selectNonstarbookingsList(nonstarbookings);
        ExcelUtil<Nonstarbookings> util = new ExcelUtil<Nonstarbookings>(Nonstarbookings.class);
        util.exportExcel(response, list, "非星级酒店预定信息数据");
    }

    /**
     * 获取非星级酒店预定信息详细信息
     */
    @RequiresPermissions("hotel:nonstarbookings:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(nonstarbookingsService.selectNonstarbookingsById(id));
    }

    /**
     * 新增非星级酒店预定信息
     */
    @RequiresPermissions("hotel:nonstarbookings:add")
    @Log(title = "非星级酒店预定信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Nonstarbookings nonstarbookings)
    {
        return toAjax(nonstarbookingsService.insertNonstarbookings(nonstarbookings));
    }

    /**
     * 修改非星级酒店预定信息
     */
    @RequiresPermissions("hotel:nonstarbookings:edit")
    @Log(title = "非星级酒店预定信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Nonstarbookings nonstarbookings)
    {
        return toAjax(nonstarbookingsService.updateNonstarbookings(nonstarbookings));
    }

    /**
     * 删除非星级酒店预定信息
     */
    @RequiresPermissions("hotel:nonstarbookings:remove")
    @Log(title = "非星级酒店预定信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(nonstarbookingsService.deleteNonstarbookingsByIds(ids));
    }

    @RequiresPermissions("hotel:nonstarbookings:confirm")
    @DeleteMapping("/confirm/{ids}")
    public AjaxResult Confirm(@PathVariable Long[] ids)
    {
        return toAjax(nonstarbookingsService.confirmNonstarbookingsByIds(ids));
    }
}

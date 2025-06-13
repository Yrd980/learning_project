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
import com.ruoyi.hotel.domain.Starhotels;
import com.ruoyi.hotel.service.IStarhotelsService;
import com.ruoyi.common.core.web.controller.BaseController;
import com.ruoyi.common.core.web.domain.AjaxResult;
import com.ruoyi.common.core.utils.poi.ExcelUtil;
import com.ruoyi.common.core.web.page.TableDataInfo;

/**
 * 星级酒店信息Controller
 * 
 * @author ningf
 * @date 2024-07-11
 */
@RestController
@RequestMapping("/starhotels")
public class StarhotelsController extends BaseController
{
    @Autowired
    private IStarhotelsService starhotelsService;

    /**
     * 查询星级酒店信息列表
     */
    @RequiresPermissions("hotel:starhotels:list")
    @GetMapping("/list")
    public TableDataInfo list(Starhotels starhotels)
    {
        startPage();
        List<Starhotels> list = starhotelsService.selectStarhotelsList(starhotels);
        return getDataTable(list);
    }

    /**
     * 导出星级酒店信息列表
     */
    @RequiresPermissions("hotel:starhotels:export")
    @Log(title = "星级酒店信息", businessType = BusinessType.EXPORT)
    @PostMapping("/export")
    public void export(HttpServletResponse response, Starhotels starhotels)
    {
        List<Starhotels> list = starhotelsService.selectStarhotelsList(starhotels);
        ExcelUtil<Starhotels> util = new ExcelUtil<Starhotels>(Starhotels.class);
        util.exportExcel(response, list, "星级酒店信息数据");
    }

    /**
     * 获取星级酒店信息详细信息
     */
    @RequiresPermissions("hotel:starhotels:query")
    @GetMapping(value = "/{id}")
    public AjaxResult getInfo(@PathVariable("id") Long id)
    {
        return success(starhotelsService.selectStarhotelsById(id));
    }

    /**
     * 新增星级酒店信息
     */
    @RequiresPermissions("hotel:starhotels:add")
    @Log(title = "星级酒店信息", businessType = BusinessType.INSERT)
    @PostMapping
    public AjaxResult add(@RequestBody Starhotels starhotels)
    {
        return toAjax(starhotelsService.insertStarhotels(starhotels));
    }

    /**
     * 修改星级酒店信息
     */
    @RequiresPermissions("hotel:starhotels:edit")
    @Log(title = "星级酒店信息", businessType = BusinessType.UPDATE)
    @PutMapping
    public AjaxResult edit(@RequestBody Starhotels starhotels)
    {
        return toAjax(starhotelsService.updateStarhotels(starhotels));
    }

    /**
     * 删除星级酒店信息
     */
    @RequiresPermissions("hotel:starhotels:remove")
    @Log(title = "星级酒店信息", businessType = BusinessType.DELETE)
	@DeleteMapping("/{ids}")
    public AjaxResult remove(@PathVariable Long[] ids)
    {
        return toAjax(starhotelsService.deleteStarhotelsByIds(ids));
    }
}
